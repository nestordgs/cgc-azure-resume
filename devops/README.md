# Devops

## Deploy Create

```bash
export resourceGroup="<your-resource-group-name>"
export accountName="<your-storage-account-name>"
export azureFunctionApp="<your-az-function-app>"
```

Steps

- Desploy Storage Account With Container & CDN
- Deploy Cosmos DB.
- Deploy Function App.
- Enable manually the "Static Website" for Storage Account.
- Purge endpoint in path `/`.
- Deploy Azure Function to Azure Function App.

command to deploy and create template for **Storage Account**

```bash
az deployment group create -g $resourceGroup -n 'acg-resume-az-stge-account-deployment' \
    --template-file devops/storage-account-template.json \
    --parameters devops/storage-account-parameters.json
```

Command to upload static fields to blob container

```bash
    az storage blob upload-batch --account-name $accountName -d '$web' -s frontend/
```

Command to deploy and create the **Cosmo DB**

```bash
az deployment group create -g $resourceGroup -n 'acg-resume-az-cosmos-db-deployment' \
    --template-file devops/cosmo-db-template.json \
    --parameters devops/cosmo-db-parameters.json
```

Command to deploy and create the **Azure Function**

```bash
az deployment group create -g $resourceGroup -n 'acg-resume-az-function-app-deployment' \
    --template-file devops/func-app-template.json \
    --parameters devops/func-app-parameters.json
```

Command to deploy *Azure Function* to *Function App*

```bash
    func azure functionapp publish $azureFunctionApp --python
```
