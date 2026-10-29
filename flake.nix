{
  description = "Cybersecurity coursework dev shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          unzip
          binwalk
          exiftool
          steghide
          zsteg
          foremost
          ffmpeg
          python3
          sqlmap
	  nmap
        ];
        shellHook = ''
  export NIX_LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
    pkgs.stdenv.cc.cc.lib
    pkgs.zlib
    pkgs.xorg.libxcb
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXrender
    pkgs.xorg.libSM
    pkgs.xorg.libICE
    pkgs.glib
    pkgs.libGL
    pkgs.fontconfig
    pkgs.freetype
  ]}"
'';	
      };
    };
}
