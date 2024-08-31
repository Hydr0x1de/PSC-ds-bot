python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
touch restart_ctx.json
touch config.toml
echo 'TOKEN = ""' > config.toml
echo 'PORT = ""' >> config.toml