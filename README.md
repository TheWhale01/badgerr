# Badgerr

Badgerr is a simple tool that adds an overlay on jellyfin media posters based on maintainerr's collections.

> __*NOTE:*__ Jellyfin is heavily asynchronous so changes can take a moment to reflect on the UI

## Configuration

You will need to have these environment variables:

 - `JELLYFIN_URL`: URL of your jellyfin server
 - `JELLYFIN_API_KEY`: API key used to change posters of your media
 - `MAINTAINERR_URL`: URL of your maintainerr server
 - `MAINTAINERR_API_KEY`: API key used to get the media that needs to be marked
 - `FONT_URL`: URL of the font to use
 - `BADGERR_TAGNAME`: The tagname used in jellyfin to mark overlayed media
 
## Launch
 
```bash
python3 main.py --config '/path/to/yaml/config'
```

> __*NOTE:*__ You can find a yaml configuration example in the `config.yaml` file

## Installation

### NixOS

```nix
# flake.nix
{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-25.11";
    badgerr = {
      url = "github:TheWhale01/badgerr";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = {nixpkgs, badgerr, ...}@inputs:
  let
    system = "x86_64-linux";
    lib = nixpkgs.lib;
    pkgs = import nixpkgs {
      system = "${system}";
    };
  in
  {
    nixosConfigurations = {
      erebos = lib.nixosSystem {
        inherit system;
        inherit pkgs;
        specialArgs = { inherit inputs; };
        modules = [
          ./configuration.nix
          badgerr.nixosModules.default
        ];
      };
    };
  };
}
```

```nix
# configuration.nix
services.badgerr = {
  enable = true;
  jellyfinUrl = "https://jellyfin.example.com";
  maintainerrUrl = "https://maintainerr.example.com";
  tagname = "badgerr-overlay";
  environmentFile = /path/to/secrets/file;
  settings = {
    text = {
      font_size = 150;
      value = "Leaving Soon";
      color = "#ffffff";
      background_color = "#e50914";
      padding_x = 40;
      padding_y = 40;
    };
    position = "top";
    image = {
      background_color = "#000000";
      background_opacity = 0;
      padding_y = 100;
    };
  };
}
```

### Docker

*Work in progress...*


## TODO

 - Better multithreading support.
 - use [jellyfin-sdk](https://pypi.org/project/jellyfin-sdk/) instead of regular requests to make API calls.
 - `docker-compose.yml` file for easier integration on other systems.
