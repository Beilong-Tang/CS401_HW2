## This scripts serves as the purpose to create argoCD

argocd app create bl-cs401-hw2 \
      --repo https://github.com/Beilong-Tang/CS401_HW2.git \
      --path . \
      --project beilong-project \
      --dest-namespace beilong \
      --dest-server https://kubernetes.default.svc \
      --sync-policy auto
# The shell will replace $USER with your username.