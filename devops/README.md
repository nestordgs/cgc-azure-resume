# Devops

## Deploy Create

```bash
export resourceGroup="1-9f6200b2-playground-sandbox"
export deploymentName="stge-acg-resume"
export accountName="stgeaccount"
```

Steps

- Desploy Storage Account With Container & CDN
- Enable manually the "Static Website" for Storage Account
- Purge endpoint in path `/`
- Deploy Cosmos DB template.
- Deploy Function App template.

command to deploy and create template for **Storage Account**

```bash
az deployment group create -g $resourceGroup -n 'acg-resume-stge-account' \
    --template-file devops/storage-account-template.json \
    --parameters devops/storage-account-parameters.json
```

## Deploy Update

command to deploy and update template for **Storage Account**

```bash
az deployment group create -g $resourceGroup -n 'acg-resume-az-stge-account' \
    --template-file devops/storage-account-template.json \
    --parameters devops/storage-account-parameters.json \
    --mode Complete
```

Command to upload static fields to blob container

```bash
    az storage blob upload-batch --account-name $accountName -d '$web' -s frontend/
```

Command to deploy and create the **Cosmo DB**

```bash
az deployment group create -g $resourceGroup -n 'acg-resume-az-cosmo-db' \
    --template-file devops/cosmo-db-template.json \
    --parameters devops/cosmo-db-parameters.json \
    --mode Complete
```

Command to deploy and create the **Azure Function**

```bash
az deployment group create -g $resourceGroup -n 'acg-resume-az-function-app' \
    --template-file devops/func-app-template.json \
    --parameters devops/func-app-parameters.json \
    --mode Complete
```
