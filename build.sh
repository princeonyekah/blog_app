set -o errexit
pip install --upgrade pip
pip install -r requirement.txt
prisma db push