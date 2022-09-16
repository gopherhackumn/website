{
  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in rec {
        devShell = pkgs.mkShell { inputsFrom = with packages; [ site ]; };
        defaultPackage = packages.site;
        packages.site = pkgs.stdenv.mkDerivation {
          name = "site";
          src = pkgs.nix-gitignore.gitignoreSource [ ] ./.;

          buildInputs = with pkgs; [ zola hugo ];
          phases = [ "unpackPhase" "buildPhase" ];
          buildPhase = "hugo -d $out";
        };
      });
}
