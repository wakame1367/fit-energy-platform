resource "aws_ecr_repository" "app" {
  name = local.project
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_s3_bucket" "infra" {
  bucket = local.project
}

resource "aws_iam_role" "lambroll_lambda_role" {
  name = "${local.project}-lambroll-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "basic_exec" {
  role       = aws_iam_role.lambroll_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "s3_access" {
  name = "${local.project}-s3-access"
  role = aws_iam_role.lambroll_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = ["s3:PutObject", "s3:GetObject", "s3:HeadObject"],
      Resource = "${aws_s3_bucket.infra.arn}/*"
    }]
  })
}

output "lambroll_lambda_role_arn" {
  value = aws_iam_role.lambroll_lambda_role.arn
}

output "ecr_url" {
  value = aws_ecr_repository.app.repository_url
}
