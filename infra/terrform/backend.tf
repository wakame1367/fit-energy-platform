terraform {
  backend "s3" {
    bucket = "tf-state-40f33dd3"
    key    = "fit-energy-platform/terraform.tfstate"
    region = "ap-northeast-1"
  }
}
