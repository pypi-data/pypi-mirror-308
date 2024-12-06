import os
import shutil
import subprocess
from pathlib import Path


def main():
    module_path = "sympla_tools/tickets/signature/ethereum_token.py"

    output_dir = "dist"
    executable_name = "tickets_signature_token_validate"

    subprocess.run(
        [
            "pyinstaller",
            "--onefile",
            "--distpath",
            output_dir,
            "--name",
            executable_name,
            module_path,
        ],
        check=True,
    )

    compiled_bin = Path(output_dir) / executable_name

    os.makedirs("bin", exist_ok=True)

    shutil.move(str(compiled_bin), f"bin/{executable_name}")

    print(f"Binário criado e disponível em 'bin/{executable_name}'")


if __name__ == "__main__":
    main()
