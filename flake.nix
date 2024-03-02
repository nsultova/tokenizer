{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };
  outputs = { nixpkgs, flake-utils, ... }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
      };
    in rec {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python3.withPackages(ps: with ps; [
            ipython jupyter spyder qtconsole
            numpy matplotlib
            pandas plotly ipywidgets notebook
            scipy keras tensorflow
            scikit-image urllib3 scikit-learn
            opencv4
            sympy
          ]))
        ];
        shellHook = ''
            export PYTHONPATH="$PYTHON_PATH:`pwd`/src"
            #jupyter notebook
            #jupyter lab
            #spyder
            #exit
        '';
      };
      devShells.${system} = {
        doc = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [ mdbook mdbook-mermaid ];
          shellHook = ''
            cd doc
            mdbook-mermaid install
            mdbook serve
          '';
        };
        get_corpus = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            lynx
            #poppler_utils wget
          ];
          shellHook = ''
            lynx --display_charset=utf-8 --dump https://nixos.org/manual/nixos/stable/index.html#ch-installation > example/corpus.txt
          '';
        };
      };
    }
  );
}
