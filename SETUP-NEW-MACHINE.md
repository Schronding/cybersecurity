# Setting up this lab on a new computer

This guide recreates the NixOS WSL environment from the old laptop on a new Windows computer, so you can continue the Juice Shop lab where you left off.

There are two ways to do it:

- **Option A — fresh install (recommended).** Install NixOS-WSL, apply the saved system configuration, and clone this repo. Everything the labs need is described in `nixos/configuration.nix` and `flake.nix`, so the result is the same setup. It takes about 30–60 minutes, mostly downloads.
- **Option B — exact copy.** Export the whole WSL disk from the old laptop and import it on the new one. You get everything, including Claude Code's settings and SSH keys, but the export file is large: the old laptop's WSL holds about 76 GB, 56 GB of it Nix packages that Option A downloads again anyway. You'd need a drive that size to carry it.

Commands marked **PowerShell** run in Windows PowerShell. Commands marked **NixOS** run in the NixOS terminal.

---

## Option A — fresh install

### 1. Install WSL (PowerShell, as administrator)

```powershell
wsl --install --no-distribution
```

Restart Windows when it asks.

### 2. Install NixOS-WSL

1. Download `nixos.wsl` from the latest release at https://github.com/nix-community/NixOS-WSL/releases/latest
2. Double-click the file, or run in PowerShell from the download folder:

   ```powershell
   wsl --install --from-file nixos.wsl
   ```
3. Open it with `wsl -d NixOS`. You are now user `nixos`.

### 3. Give the new machine access to GitHub (NixOS)

The repo is cloned over SSH, so the new machine needs its own key:

```bash
ssh-keygen -t ed25519 -C "new-pc"
cat ~/.ssh/id_ed25519.pub
```

Copy the printed line into GitHub → Settings → SSH and GPG keys → New SSH key.

### 4. Clone this repo (NixOS)

```bash
sudo nix-channel --update
mkdir -p ~/repos
nix-shell -p git --run 'git clone git@github.com:Schronding/cybersecurity.git ~/repos/cybersecurity'
```

### 5. Apply the system configuration (NixOS)

`nixos/configuration.nix` is a copy of the old laptop's `/etc/nixos/configuration.nix`. It enables flakes, direnv, Docker, nix-ld, and the tools used across the labs.

1. Check the release line of the new install first:

   ```bash
   grep stateVersion /etc/nixos/configuration.nix
   ```
2. Copy the saved configuration over it:

   ```bash
   sudo cp ~/repos/cybersecurity/nixos/configuration.nix /etc/nixos/configuration.nix
   ```
3. Open it with `sudo nano /etc/nixos/configuration.nix`. If the new install's `system.stateVersion` from step 1 was different, put that value back. That line must keep the value of the machine's *first* install.
4. Build it:

   ```bash
   sudo nixos-rebuild switch
   ```
5. Restart WSL so the Docker group and direnv take effect. In PowerShell run `wsl --shutdown`, then open NixOS again.

### 6. Load the lab tools (NixOS)

```bash
cd ~/repos/cybersecurity
direnv allow
```

The first time, this downloads nuclei, ZAP, Firefox, sqlmap, nmap and the rest from `flake.nix`, which takes several minutes. After that, the tools load by themselves whenever you enter the folder. Check them:

```bash
nuclei -version
zap -cmd -version
sqlmap --version
```

Then download the nuclei templates:

```bash
nuclei -update-templates
```

### 7. Start Juice Shop (NixOS)

```bash
docker run --rm -p 127.0.0.1:3000:3000 bkimminich/juice-shop
```

Leave that terminal open, and check that http://127.0.0.1:3000 loads.

### 8. Claude Code (optional, NixOS)

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Your Claude Code settings live outside the repo, in `~/.claude` on the old laptop. To bring them along, copy these from the old laptop through File Explorer at `\\wsl$\NixOS\home\nixos\.claude\` to the same place on the new one:

- `CLAUDE.md` and the `rules/` folder: your instructions about NixOS.
- `settings.json`: includes the direnv hook so Claude's commands see the flake's tools.
- `projects/-home-nixos-repos-cybersecurity/memory/`: what Claude remembers about you and this repo, such as going step by step.

Don't copy `.credentials.json`; log in again instead. In VS Code, install the **WSL** and **Claude Code** extensions.

---

## Option B — exact copy of the old WSL

On the **old** laptop (PowerShell). The export can be tens of gigabytes, so save it to a drive with enough space:

```powershell
wsl --shutdown
wsl --export NixOS D:\nixos-backup.tar
```

On the **new** computer (PowerShell), after `wsl --install --no-distribution` and a restart:

```powershell
mkdir C:\WSL\NixOS
wsl --import NixOS C:\WSL\NixOS D:\nixos-backup.tar
wsl -d NixOS
```

Everything comes along, including repos, keys, Claude settings and Docker images. Run `git pull` in `~/repos/cybersecurity` in case the repo changed after the export.

---

## Where the Juice Shop lab stands

- **Module 1 (nuclei):** scan done. The results are in `juice_shop/nuclei_juice.jsonl` and `juice_shop/nuclei_md/`. Still to write: the list of real findings vs false positives.
- **Module 2 (ZAP):** ZAP's session was lost when it closed, because it was a temporary session. Redo the quick part:
  1. In ZAP, open Quick Start → Manual Explore with `http://127.0.0.1:3000`, and browse the site.
  2. In the Sites tab, right-click the site → Include in Context → Default Context.
  3. Attack → Spider..., then Attack → AJAX Spider... with **2 browser windows** and a 10-minute limit.
  4. Take the Site Tree screenshot.

  **To keep ZAP's work this time**, use File → Persist Session... right after opening ZAP and save it inside `juice_shop/`. Then closing ZAP no longer deletes it.

  `juice_shop/zap_snapshot/` keeps the passive alerts and spider results from the lost session, for reference.
- **Next steps after that:** pick 3 passive alerts, run the active scan, write the comparison table, then Module 3 (sqlmap).
- Questions answered so far are in `juice_shop/doubts.md`. Your own log is `juice_shop/report.md`.
