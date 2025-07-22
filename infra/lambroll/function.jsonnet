{
  FunctionName: 'fit-energy-scraper',
  PackageType: 'Image',
  Role: 'arn:aws:iam::086854724267:role/fit-energy-platform-lambroll-lambda-role',
  Code: {
    ImageUri: '086854724267.dkr.ecr.ap-northeast-1.amazonaws.com/fit-energy-platform:sha-3f987f9c1446c9e2b2206bfed4d9f6c9d86c6659'
  },
  MemorySize: 512,
  Timeout: 300,
  Environment: {
    Variables: {
      S3_BUCKET: 'fit-energy-data'
    }
  },
}