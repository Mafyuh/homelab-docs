import os
import re
import shutil

# Paths
posts_dir = r"C:\Users\admin\Documents\Git Repos\homelab-docs\content\docs"  # Hugo content posts directory
attachments_dir = r"C:\Users\admin\Documents\Obsidian Vault\attachments"         # Obsidian attachments directory
static_images_dir = r"C:\Users\admin\Documents\Git Repos\homelab-docs\static\images"  # Hugo static images directory

# Step 1: Process each markdown file in the Hugo posts directory (not Obsidian)
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format [[Pasted%20image%20...%20.png]]
        images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces
            markdown_image = f"[Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            
            # Step 4: Copy the image to the Hugo static/images directory if it exists (Hugo only)
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)

        # Step 5: Write the updated content back to the Hugo markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")
