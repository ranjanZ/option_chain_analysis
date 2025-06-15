terraform {
  backend "s3" {
    # These will be overridden by -backend-config during init
    bucket         = ""
    key            = ""
    region         = ""
  }
}
