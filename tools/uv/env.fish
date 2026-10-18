if not contains "$HOME/Documents/SVILUPPO/rag-platform/tools/uv" $PATH
    # Prepending path in case a system-installed binary needs to be overridden
    set -x PATH "$HOME/Documents/SVILUPPO/rag-platform/tools/uv" $PATH
end
