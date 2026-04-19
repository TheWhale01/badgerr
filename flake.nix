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
        ln -sf ${virtualEnv} ./.venv
      '';
    };
    nixosModules.default = { config, lib, pkgs, ... }:
    let
      format = pkgs.format.yaml {};
      cfg = config.services.badgerr;
    in
    {
      options.services.badgerr = {
        enable = lib.mkEnableOption "Whether to enable the badgerr service.";
        user = lib.mkOption {
       	  type = lib.types.str;
       	  default = "badgerr";
       	  description = "User to run the service as.";
       	};
        group = lib.mkOption {
       	  type = lib.types.str;
       	  default = "badgerr";
       	  description = "Group to run the service as.";
       	};
        jellyfinUrl = lib.mkOption {
       	  type = lib.types.str;
       	  default = "http://127.0.0.1:8096";
       	  description = "Url of your jellyfin server.";
       	};
        maintainerrUrl = lib.mkOption {
       	  type = lib.types.str;
       	  default = "http://127.0.0.1:6246";
       	  description = "Url of your maintainerr service.";
       	};
       	tagname = lib.mkOption {
       	  type = lib.types.str;
       	  default = "badgerr-overlay";
       	  description = "Name of the tag used to retrieve media inside Jellyfin.";
       	};
       	environmentFile = lib.mkOption {
       	  type = lib.types.path;
       	  default = null;
       	  description = "Environment file to declare secrets like JELLYFIN_API and MAINTAINERR_API.";
       	};
       	settings = lib.mkOption {
       	  type = format.type;
       	  default = {};
       	  description = "Describes the style and position of the overlay to add to Jellyfin media posters.";
       	};
      };
    };
  };
}
