{
  FunctionName: 'fit-energy-scraper',
  PackageType: 'Image',
  Role: '{{ must_env `ROLE_ARN` }}',
  Code: {
    ImageUri: '{{ must_env `IMAGE_URI` }}'
  },
  MemorySize: 512,
  Timeout: 300,
  Environment: {
    Variables: {
      S3_BUCKET: '{{ must_env `S3_BUCKET` }}'
    }
  }
}
