# Connect opendocket.dev to GitHub Pages

1. In your domain registrar, add these DNS records:

   | Type  | Name | Value              |
   |-------|------|--------------------|
   | A     | @    | 185.199.108.153    |
   | A     | @    | 185.199.109.153    |
   | A     | @    | 185.199.110.153    |
   | A     | @    | 185.199.111.153    |
   | CNAME | www  | Anurag-Mohanty.github.io |

2. In GitHub repo Settings > Pages:
   - Custom domain: `opendocket.dev`
   - Enforce HTTPS: checked

3. DNS propagation takes up to 48 hours.
   Test with: `dig opendocket.dev`
