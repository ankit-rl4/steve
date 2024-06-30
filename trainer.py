from config import subscription_id, resource_group, workspace_name
from azureml.core import Workspace, Experiment, ScriptRunConfig

# Load Azure ML workspace
ws = Workspace.get(name=workspace_name, subscription_id=subscription_id, resource_group=resource_group)

# Create or retrieve an experiment
experiment = Experiment(workspace=ws, name='ex1')

# Create a script run configuration
src = ScriptRunConfig(source_directory='./',
                      script='train.py',
                      compute_target='steve3000',
                      environment=ws.environments['stevespace'])

# Submit the experiment
run = experiment.submit(src)
