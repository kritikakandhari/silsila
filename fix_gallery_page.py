import subprocess
import re

# 1. Get the 9-item gallery HTML from the older commit 4131afa
result = subprocess.run(["git", "show", "4131afa:index.html"], capture_output=True, text=True, encoding='utf-8')
old_index_html = result.stdout

match = re.search(r'<section class="gallery" id="gallery">.*?</section>', old_index_html, re.DOTALL)
if not match:
    print("Failed to find gallery section in old commit.")
    exit(1)
full_gallery_html = match.group(0)

# 2. Read faq.html to use as a template for gallery.html
with open('faq.html', 'r', encoding='utf-8') as f:
    faq_content = f.read()

# Replace title and description
gallery_html = re.sub(r'<title>FAQ — SILSILA.*?</title>', '<title>Gallery — SILSILA | Indian Fusion Kitchen, Edmonton</title>', faq_content)
gallery_html = re.sub(r'<meta name="description".*?>', '<meta name="description" content="View Silsila\'s gallery of handcrafted flavours, authentic heritage, and moments in motion.">', gallery_html)

# Insert the full gallery HTML in place of faq-section
gallery_html = re.sub(r'<section class="faq-section">.*?</section>', full_gallery_html, gallery_html, flags=re.DOTALL)

# Add Lightbox HTML/JS from old_index_html (it was at the end of the file)
match_js = re.search(r'(// ---- Gallery Wall & Designer Lightbox ----.*?)</script>', old_index_html, re.DOTALL)
match_html = re.search(r'<!-- Designer Gallery Lightbox Modal -->.*</div>', old_index_html, re.DOTALL)

if match_js and match_html:
    lb_js = match_js.group(1) + '</script>'
    lb_html = match_html.group(0)
    gallery_html = gallery_html.replace('</body>', lb_js + '\n' + lb_html + '\n</body>')

# Update nav links in gallery_html
gallery_html = gallery_html.replace('href="index.html#gallery"', 'href="gallery.html"')
gallery_html = gallery_html.replace('href="#gallery"', 'href="gallery.html"')

# Write gallery.html
with open('gallery.html', 'w', encoding='utf-8') as f:
    f.write(gallery_html)
print("Created gallery.html with all 9 photos.")

# 3. Update nav links in index.html, faq.html, menu.html
def update_nav(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('href="index.html#gallery"', 'href="gallery.html"')
    content = content.replace('href="#gallery"', 'href="gallery.html"')
    # Also change the id of the gallery section in index.html to avoid conflict if any
    if filename == 'index.html':
        content = content.replace('<section class="gallery" id="gallery">', '<section class="gallery" id="home-gallery">')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_nav('index.html')
update_nav('faq.html')
update_nav('menu.html')
print("Updated all nav links.")
