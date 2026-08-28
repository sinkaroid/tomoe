use crate::error::TomoeError;
use crate::info;
use ::image::GenericImageView;
use printpdf::{
    BuiltinFont, ColorBits, ColorSpace, Image as PdfImage, ImageTransform, ImageXObject, Mm,
    PdfDocument, Px,
};
use std::fs::{self, File};
use std::io::{BufWriter, Write};
use std::path::{Path, PathBuf};

/// Compiles all downloaded images in `dir` into a single PDF file named `<title>.pdf`.
pub fn compile_pdf(
    dir: &Path,
    gallery_id: &str,
    gallery_title: &str,
) -> Result<PathBuf, TomoeError> {
    info!(
        "Compiling PDF for gallery ID {} in {:?}...",
        gallery_id, dir
    );

    let mut image_paths = Vec::new();
    if dir.exists() {
        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            let path = entry.path();
            let is_image = path.is_file()
                && path
                    .extension()
                    .map(|e| e.to_string_lossy().to_lowercase())
                    .map(|ext| ext == "jpg" || ext == "jpeg" || ext == "png" || ext == "webp")
                    .unwrap_or(false);
            if is_image {
                image_paths.push(path);
            }
        }
    }

    if image_paths.is_empty() {
        return Err(TomoeError::PdfError(
            "No images found in directory to compile into PDF".to_string(),
        ));
    }

    // Sort image paths naturally by filename
    image_paths.sort_by(|a, b| a.file_name().cmp(&b.file_name()));

    let sanitized_title = sanitize_filename(gallery_title);
    let output_pdf_path = dir.join(format!("{}.pdf", sanitized_title));

    // Create PDF document with standard A4 page size: 210mm x 297mm
    let doc_title = format!("Tomoe Gallery {}", gallery_title);
    let (doc, page1, layer1) = PdfDocument::new(&doc_title, Mm(210.0), Mm(297.0), "Layer 1");

    let font_bold = doc
        .add_builtin_font(BuiltinFont::HelveticaBold)
        .map_err(|e| TomoeError::PdfError(e.to_string()))?;

    let total_pages = image_paths.len();

    for (idx, img_path) in image_paths.iter().enumerate() {
        let img = ::image::open(img_path).map_err(|e| {
            TomoeError::PdfError(format!("Failed to open image {:?}: {}", img_path, e))
        })?;

        let (w_px, h_px) = img.dimensions();
        let img_ratio = (w_px as f32) / (h_px as f32);

        let current_layer = if idx == 0 {
            doc.get_page(page1).get_layer(layer1)
        } else {
            let (page_idx, layer_idx) = doc.add_page(Mm(210.0), Mm(297.0), "Layer 1");
            doc.get_page(page_idx).get_layer(layer_idx)
        };

        // Determine bounding box for the image on this page
        let (box_w, box_h, box_x, box_y) = if idx == 0 {
            // First page: has header at the top
            // Header is at y = 265mm. Bounding box: y from 20mm to 250mm (height 230mm)
            // If total_pages == 1, it also has a footer at y = 15mm. Bounding box: y from 30mm to 250mm (height 220mm)
            if total_pages == 1 {
                (190.0, 220.0, 10.0, 30.0)
            } else {
                (190.0, 230.0, 10.0, 20.0)
            }
        } else if idx == total_pages - 1 {
            // Last page: has footer at the bottom (y = 15mm). Bounding box: y from 30mm to 287mm (height 257mm)
            (190.0, 257.0, 10.0, 30.0)
        } else {
            // Intermediate page: full page box (10mm margins). Bounding box: y from 10mm to 287mm (height 277mm)
            (190.0, 277.0, 10.0, 10.0)
        };

        // Render header on first page
        if idx == 0 {
            let title_text = gallery_id;
            let text_size = 24.0;
            let approx_width_mm = (title_text.len() as f32) * text_size * 0.6 * 0.352778;
            let text_x = (210.0 - approx_width_mm) / 2.0;
            let text_y = 265.0;

            current_layer.begin_text_section();
            current_layer.set_font(&font_bold, text_size);
            current_layer.set_text_cursor(Mm(text_x), Mm(text_y));
            current_layer.write_text(title_text, &font_bold);
            current_layer.end_text_section();
        }

        // Render footer on last page
        if idx == total_pages - 1 {
            let footer_text = "crates.io/crates/tomoe";
            let text_size = 12.0;
            let approx_width_mm = (footer_text.len() as f32) * text_size * 0.5 * 0.352778;
            let text_x = (210.0 - approx_width_mm) / 2.0;
            let text_y = 15.0;

            current_layer.begin_text_section();
            current_layer.set_font(&font_bold, text_size);
            current_layer.set_text_cursor(Mm(text_x), Mm(text_y));
            current_layer.write_text(footer_text, &font_bold);
            current_layer.end_text_section();
        }

        // Calculate scaled dimensions to fit inside the bounding box
        let box_ratio = box_w / box_h;
        let (w_scaled, h_scaled) = if img_ratio > box_ratio {
            // Limited by width
            let w = box_w;
            let h = box_w / img_ratio;
            (w, h)
        } else {
            // Limited by height
            let h = box_h;
            let w = box_h * img_ratio;
            (w, h)
        };

        let offset_x = box_x + (box_w - w_scaled) / 2.0;
        let offset_y = box_y + (box_h - h_scaled) / 2.0;

        let rgb8 = img.to_rgb8();
        let image_xobject = ImageXObject {
            width: Px(w_px as usize),
            height: Px(h_px as usize),
            color_space: ColorSpace::Rgb,
            bits_per_component: ColorBits::Bit8,
            interpolate: false,
            image_data: rgb8.into_raw(),
            image_filter: None,
            smask: None,
            clipping_bbox: None,
        };
        let pdf_image = PdfImage::from(image_xobject);

        let transform = ImageTransform {
            translate_x: Some(Mm(offset_x)),
            translate_y: Some(Mm(offset_y)),
            scale_x: Some((w_scaled * 2.834_645_7) / (w_px as f32)),
            scale_y: Some((h_scaled * 2.834_645_7) / (h_px as f32)),
            dpi: Some(72.0),
            ..Default::default()
        };

        pdf_image.add_to_layer(current_layer, transform);
        print!("\r[PDF] Compiling page {}/{}", idx + 1, total_pages);
        let _ = std::io::stdout().flush();
    }

    println!("\nPDF compilation complete!");

    let file = File::create(&output_pdf_path)?;
    let mut writer = BufWriter::new(file);
    doc.save(&mut writer)
        .map_err(|e| TomoeError::PdfError(e.to_string()))?;

    let pdf_size_mb = output_pdf_path.metadata()?.len() as f64 / 1024.0 / 1024.0;
    println!(
        "Successfully rendered PDF: {} ({:.2} MB)",
        output_pdf_path
            .file_name()
            .unwrap_or_default()
            .to_string_lossy(),
        pdf_size_mb
    );

    Ok(output_pdf_path)
}

/// Helper function to sanitize titles for filesystem directory creation.
fn sanitize_filename(name: &str) -> String {
    let cleaned = name
        .chars()
        .map(|c| {
            if c.is_alphanumeric() || c == '-' {
                c
            } else {
                ' '
            }
        })
        .collect::<String>();
    cleaned.split_whitespace().collect::<Vec<_>>().join("_")
}
