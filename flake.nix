{
  description = "Automatically apply overlay on Jellyfin based on Maintainerr's collections";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    uv2nix.url = "github:pyproject-nix/uv2nix";
    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
    build-systems.url = "github:pyproject-nix/build-system-pkgs";
  };
  outputs = {
    nixpkgs,
    uv2nix,
    pyproject-nix,
    build-systems,
    ...
  }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
    pythonSet = pkgs.callPackage pyproject-nix.build.packages {
      python = pkgs.python312;
    };
    overlay = workspace.mkPyprojectOverlay {
      sourcePreference = "wheel";
    };
    pythonEnv = pythonSet.overrideScope (pkgs.lib.composeManyExtensions [
      build-systems.overlays.default
      overlay
    ]);
    virtualEnv = pythonEnv.mkVirtualEnv "badgerr-virtualenv" workspace.deps.default;
  in
  {
    packages.${system}.default = virtualEnv;
    apps.${system}.default = {
      type = "app";
      program = "${virtualEnv}/bin/badgerr";
    };
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        pkgs.uv
        virtualEnv
      ];
      shellHook = ''
        ln -sf ${virtualEnv} .venv
      '';
    };
  };
}
