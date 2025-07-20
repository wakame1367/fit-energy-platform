resource "aws_ecr_repository" "app" {
  name = local.project
  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_url" {
  value = aws_ecr_repository.app.repository_url
}
