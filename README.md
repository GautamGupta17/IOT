# Build and deploy

```
gcloud builds submit --tag gcr.io/bionic-charge-355520/test_iot  --project=bionic-charge-355520 
```

```
gcloud run deploy --image gcr.io/bionic-charge-355520/test_iot --platform managed  --project=bionic-charge-355520  --allow-unauthenticated
```