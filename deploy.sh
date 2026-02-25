#!/bin/bash

FUNCTION_NAME=util
MEMORY=128Mi

make -B test

if [ $? -eq 0 ]; then 

	source config/config.sh

	gcloud config set project ${PROJECT_NAME}

	gcloud functions deploy ${FUNCTION_NAME} \
	--memory ${MEMORY} \
	--entry-point main \
	--runtime python310 \
	--trigger-http \
	--region ${LOCATION} \
	--ingress-settings all \
	--no-allow-unauthenticated \
	--set-env-vars PROJECT=${PROJECT_NAME},LOCATION=${LOCATION},SERVICE_ACCOUNT_EMAIL=${SERVICE_ACCOUNT_EMAIL} 

else
	echo "        _           _"
	echo "      (\`-\`;--\`\`\`--;\`-\`)"
	echo "       \\.'         './"
	echo "       /             \\"
	echo "       ;   0     0   ;"
	echo "      /| =         = |\\"
	echo "     ; \\   '._Y_.'   / ;"
	echo "    ;   \`-._ \\|/ _.-'   ;"
	echo "   ;        \`---\`        ;"
	echo "   ;    \`---.   .---\`    ;"
	echo "   /;  '--._ \\ / _.--   ;\\"
	echo "  :  \`.   \`/|| ||\\\`   .'  :"
	echo "   '.  '-._       _.-'   .'        jgs"
	echo "   (((-'\`  \`-----\`   \`'-)))"

fi