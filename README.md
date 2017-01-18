Example run:


scrapy crawl avito --output=data.csv --output-format=csv

scrapy crawl avito --set FEED_URI=s3://<key>:<secret>@<bucket>/<path-to-export-file> --set IMAGES_STORE=s3://<bucket>/<path-to-directory> --set AWS_ACCESS_KEY_ID=<key> --set AWS_SECRET_ACCESS_KEY=<secret>
