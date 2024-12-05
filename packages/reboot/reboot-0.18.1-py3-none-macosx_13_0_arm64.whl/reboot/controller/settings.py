# The ports that user containers will be asked to use to expose their Reboot
# servers. We will expose these ports via k8s Deployment/Service as well.
USER_CONTAINER_GRPC_PORT = 50051
USER_CONTAINER_WEBSOCKET_PORT = 50052

# On Kubernetes we use labels to identify which pods are Reboot consensuses,
# and what their consensuses are called. This defines what those label is
# called.
IS_REBOOT_CONSENSUS_LABEL_NAME = 'reboot.dev/is-reboot-consensus'
IS_REBOOT_CONSENSUS_LABEL_VALUE = 'true'
REBOOT_CONSENSUS_ID_LABEL_NAME = 'reboot.dev/reboot-consensus-id'

# On Kubernetes, how can we identify the Istio ingress gateways?
# ISSUE(1529): this should likely be something a cluster operator can configure.
#              The following are the settings that our LocalKubernetes gets when
#              it installs Istio using Istio's `demo` profile.
ISTIO_INGRESSGATEWAY_NAMESPACE = 'istio-system'
ISTIO_INGRESSGATEWAY_NAME = 'istio-ingressgateway'
# By "internal port" we mean the port that traffic already inside the Kubernetes
# cluster should use to access the Istio ingress gateway. This may differ from
# the port that external traffic from outside the Kubernetes cluster uses to
# reach the load balancer.
#
# TODO(rjh): change this to 9990 to be more unique and match the default
#            insecure port?
ISTIO_INGRESSGATEWAY_INTERNAL_PORT = 8080
ISTIO_INGRESSGATEWAY_LABEL_NAME = 'istio'
ISTIO_INGRESSGATEWAY_LABEL_VALUE = 'ingressgateway'

# In an Istio `VirtualService`, how do we address all Istio sidecars?
ISTIO_ALL_SIDECARS_GATEWAY_NAME = 'mesh'

# Labels that need to be set on a namespace in order for Istio to do sidecar
# injection.
ISTIO_NAMESPACE_LABELS = {
    # Required to be set in order for Istio to inject sidecars into a Reboot
    # namespace.
    'istio-injection': 'enabled',
}

# The reboot system requires two Kubernetes namespaces: one for the system
# itself, and one to place `ApplicationDeployment`s. What are these namespaces
# called?
REBOOT_SYSTEM_NAMESPACE = 'reboot-system'
REBOOT_APPLICATION_DEPLOYMENT_NAMESPACE = 'reboot-application-deployments'

# On Kubernetes, some objects need fixed names.
REBOOT_MESH_VIRTUAL_SERVICE_NAME = 'network-managers-mesh-virtual-service'
REBOOT_GATEWAY_VIRTUAL_SERVICE_NAME = 'network-managers-gateway-virtual-service'
REBOOT_MESH_ROUTING_FILTER_NAME = 'network-managers-mesh-routing-envoy-filter'
REBOOT_GATEWAY_ROUTING_FILTER_NAME = 'network-managers-gateway-routing-envoy-filter'
REBOOT_GATEWAY_NAME = 'reboot-gateway'

# On Kubernetes, the Reboot system will offer a fixed hostname that clients
# use when they want to talk to any Reboot service.
REBOOT_ROUTABLE_HOSTNAME = 'reboot-service'

### Environment variables.
# We use environment variables when we need to communicate information between
# processes. Our naming convention is as follows:
#   `ENVVAR_<SOMETHING>` is the name of an environment variable.
#   `<SOMETHING>_<VALUE-NAME>` is one VALUE the `SOMETHING` environment
#    variable might take.

# Application ID injected via an environment variable.
ENVVAR_REBOOT_APPLICATION_ID = 'REBOOT_APPLICATION_ID'
# Consensus ID injected via an environment variable.
ENVVAR_REBOOT_CONSENSUS_ID = 'REBOOT_CONSENSUS_ID'

# Kubernetes pod metadata injected via environment variables.
ENVVAR_KUBERNETES_POD_UID = 'REBOOT_KUBERNETES_POD_UID'
ENVVAR_KUBERNETES_POD_NAME = 'REBOOT_KUBERNETES_POD_NAME'
ENVVAR_KUBERNETES_POD_NAMESPACE = 'REBOOT_KUBERNETES_POD_NAMESPACE'
ENVVAR_KUBERNETES_SERVICE_ACCOUNT = 'REBOOT_KUBERNETES_SERVICE_ACCOUNT'

# Gives the mode in which a Reboot application is expected to be started.
# Present on any Reboot config pod.
ENVVAR_REBOOT_MODE = 'REBOOT_MODE'
REBOOT_MODE_CONFIG = 'config'  # Start the server as a config server.

# Gives the port on which a config-mode server is expected to start serving.
# Present on any Reboot config pod.
ENVVAR_REBOOT_CONFIG_SERVER_PORT = 'REBOOT_CONFIG_SERVER_PORT'

# Gives the port on which an `rbt serve` application is expected to serve its
# application.
ENVVAR_PORT = 'PORT'

# The name of the Kubernetes storage class that Reboot should use for its
# state storage.
REBOOT_STORAGE_CLASS_NAME = 'reboot-storage'
