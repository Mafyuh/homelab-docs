import os
import re
import shutil

# Paths
posts_dir = os.path.expanduser("/home/mafyuh/homelab-docs/content/docs")
attachments_dir = os.path.expanduser("/home/mafyuh/Documents/Obsidian Vault/attachments")
static_images_dir = os.path.expanduser("/home/mafyuh/homelab-docs/static/images")

# Process each markdown file in the Hugo posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Find all image links in the format [[Pasted%20image%20...%20.png]]
        images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        
        # Replace image links and ensure URLs are correctly formatted
        for image in images:
            markdown_image = f"[Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            
            # Copy the image to the Hugo static/images directory if it exists
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)

        # Write the updated content back to the Hugo markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")