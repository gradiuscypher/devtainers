FROM ubuntu as base_devtainer
RUN apt update &&\
    apt install -y python3 curl tmux vim zsh git &&\
    curl -sS https://starship.rs/install.sh | sh -s -- --yes &&\
    chsh -s $(which zsh)
RUN echo 'eval "$(starship init zsh)"' >> /root/.zshrc
RUN echo 'export LC_ALL=en_IN.UTF-8' >> /root/.zshrc
RUN echo 'export LANG=en_IN.UTF-8' >> /root/.zshrc
RUN mkdir -p /root/.tmux/themes
ADD configs/.tmux.conf /root
ADD configs/tomorrow-night-eighties.tmux /root/.tmux/themes

CMD ["sleep", "infinity"]
