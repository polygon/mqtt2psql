{
  description = "MQTT to PSQL bridge, specialized for my use-cases";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.05";

  outputs = { self, nixpkgs }: 
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
    python-env = pkgs.python310.withPackages (p: with p; [
      paho-mqtt
      psycopg2
      ipython
    ]);
  in
  {

    packages.x86_64-linux.mqtt2psqlbin = pkgs.writeShellScript "mqtt2psql" ''
      cd ${self}
      ${python-env}/bin/python -m mqtt2psql.mqtt2psql
    '';
    defaultPackage.x86_64-linux = self.packages.x86_64-linux.mqtt2psqlbin;
    devShells.x86_64-linux.default = pkgs.mkShell {
      inputsFrom = [ self.packages.x86_64-linux.mqtt2psqlbin ];
      buildInputs = [ python-env ];
    };
  };
}
