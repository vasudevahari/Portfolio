# Portfolio SEO setup

This is a plain HTML site. Publish the repository root containing `index.html`,
`img.jpg`, and `robots.txt`. No framework, API key, or paid SEO service is needed.

## Set your public URL before publishing

The configured live URL is https://vasudevahari.netlify.app/. Canonical metadata,
Open Graph URL, structured data, robots.txt and sitemap.xml use this address.
The original Google verification file is included at
`google3b7702583b872784.html`. Publish it unchanged with the rest of the site.

For the supplied verification file, open
https://vasudevahari.netlify.app/google3b7702583b872784.html after deployment,
then click **Verify** using the **HTML file** method in Google Search Console.
Submit https://vasudevahari.netlify.app/sitemap.xml and inspect the homepage.
The optional HTML-tag instructions below are an alternative verification method;
you do not need them when the supplied HTML file verification succeeds.

With Python 3 installed, run from the repository root:

```sh
python scripts/configure-seo.py https://YOUR-ACTUAL-SITE-URL/
```

Use the final preferred HTTPS homepage URL, including a subdirectory if applicable.
The script writes static metadata into `index.html`, generates `sitemap.xml`, adds
its absolute URL to `robots.txt`, and saves the setting in `seo-config.json`.
It preserves other page content. Rerunning without arguments uses the saved config.
Commit the generated files and publish them. Repeat with the new URL if you move domains.
The sitemap includes only the homepage because all sections are on that page.

## Google Search Console (manual)

1. Open https://search.google.com/search-console and sign in to your Google account.
2. Add a **URL-prefix** property with your exact published HTTPS URL.
3. Choose **HTML tag** under ownership verification. Copy only the `content` value
   from Google's `<meta name="google-site-verification" content="...">` tag.
4. Run:

   ```sh
   python scripts/configure-seo.py --verification YOUR_GOOGLE_CONTENT_VALUE
   ```

5. Commit and publish `index.html` and `seo-config.json`. Click **Verify** in Search
   Console after the live homepage contains the tag. Leave the tag in place.
6. Open **Sitemaps**, submit the full public URL ending in `/sitemap.xml`.
7. Use **URL Inspection** on the homepage, test the live URL and request indexing.

If you own a custom domain, a **Domain** property uses the DNS TXT record Google
provides instead. Add it at your domain's DNS provider; no HTML tag is needed.

The verification value is proof of site ownership, not an SEO API key. You can also
send the real public URL and Google's HTML tag to your coding assistant for insertion.
Indexing and ranking are not guaranteed.

## Checks after publishing

- Open the homepage, `/robots.txt`, and `/sitemap.xml` (under your site's base path).
- View page source: title, description, canonical, Open Graph, Twitter metadata,
  and JSON-LD should occur once, with the real public URL.
- Run https://pagespeed.web.dev/ for performance and Core Web Vitals checks.
- Check mobile widths 320, 375, 768, 1024, and 1440 pixels, navigation and reduced motion.
- Test schema with https://validator.schema.org/ and https://search.google.com/test/rich-results.

The existing portrait is about 30 KB and stays a JPEG to preserve the supplied image.
It has descriptive alt text and loads eagerly because it is above the fold.
Scenic CSS images are decorative; their CDN URLs request automatic format selection
and reduced quality. Actual performance scores and device rendering must be measured
on the deployed site; this commit does not certify those measurements.
