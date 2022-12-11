# 1) Set environmental variables (sign in to AWS console -> click on username -> security credentials -> create access key)

# IMPORTANT: these are dummy keys, replace them with your own before executing
environment:
	export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
	export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# 2) Build AWS infrastructure
build:
	terraform init
	terraform plan
	terraform apply

# 3) Destroy AWS infrastructure
destroy:
	terraform destroy