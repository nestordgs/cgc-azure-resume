## Deploy Create

resourceGroup="1-8c3a13d6-playground-sandbox"
deploymentName="stge-acg-resume"

Steps

- Desploy Storage Account With Container
- Enable manually the "Static Website" for Storage Account
- Deploy CDN

command to deploy and create template for **Storage Account**

```bash
az deployment group create -g $resourceGroup -n $deploymentName \
    --template-file devops/storage-account-template.json \
    --parameters devops/storage-account-parameters.json
```

## Deploy Update
command to deploy and update template for **Storage Account**

```bash

az deployment group create -g $resourceGroup -n $deploymentName \
    --template-file nestordgs/devops/storage-account-template.json \
    --parameters nestordgs/devops/storage-account-parameters.json \
    --mode Complete
```

