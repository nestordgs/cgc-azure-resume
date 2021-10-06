## Deploy Create
command to deploy and create template for **Storage Account**

```bash
az deployment group create -g $resourceGroup -n $deploymentName \
    --template-file nestordgs/devops/storage-account-template.json \
    --parameters nestordgs/devops/storage-account-parameters.json
```

## Deploy Update
command to deploy and update template for **Storage Account**

```bash

az deployment group create -g $resourceGroup -n $deploymentName \
    --template-file nestordgs/devops/storage-account-template.json \
    --parameters nestordgs/devops/storage-account-parameters.json \
    --mode Complete
```

