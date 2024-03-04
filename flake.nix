{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
      #url = "github:DerDennisOP/nixpkgs/wikipedia2vec";
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
            scipy keras tensorflow dm-tree transformers
            scikit-image urllib3 scikit-learn
            opencv4
            sympy
            joblib marisa-trie #wikipedia2vec
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
            mkdir example
            lynx --display_charset=utf-8 --dump https://nixos.org/manual/nixos/stable/index.html#ch-installation > example/corpus.txt
          '';
        };
      };
    }
  );
}
