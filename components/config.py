#encoding=utf8

LANGUAGES = {
        "en" : "English",
        "da" : "Dansk",
        "de" : "Deutsch"
        }

cfg = {}

cfg['runmode'] = "dev"
#cfg['runmode'] = "prod"
if cfg['runmode'] == "prod":
    cfg['host'] = '0.0.0.0'
    cfg['app_root']  = "/data/www/virtual/example.com.com/wc/src/myapp"
    cfg['static_root'] = "%s/static" % (cfg['app_root'])
    cfg['product_image_folder']   = "%s/product_images" % (cfg['static_root'])
    cfg['upload_root']  = "%s/upload" % (cfg['app_root'])

    cfg["site_url"] = "http://example.com/"

    cfg['dbhost'] = "localhost"
    cfg['dbport'] = "5432"
    
elif cfg["runmode"] == "dev":
    ...

else:
    print ("ERROR: Unknown runmode")
    import sys
    sys.exit(1)