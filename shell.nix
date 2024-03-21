let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  packages = with pkgs; [
    python3
    python311Packages.pip
    python311Packages.requests
  ];
  shellHook = ''
    if [ ! -d ".venv" ]; then
      # Command to run if directory does not exist
      python -m venv .venv
    fi
    source .venv/bin/activate
  '';
}
