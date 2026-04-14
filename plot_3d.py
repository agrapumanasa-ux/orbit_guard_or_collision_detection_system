import plotly.graph_objects as go

def plot_objects(objects, trajectories):
    fig = go.Figure()

    for obj, traj in zip(objects, trajectories):
        fig.add_trace(go.Scatter3d(
            x=[obj.position[0]],
            y=[obj.position[1]],
            z=[obj.position[2]],
            mode='markers',
            name=obj.id
        ))

        fig.add_trace(go.Scatter3d(
            x=traj[:,0],
            y=traj[:,1],
            z=traj[:,2],
            mode='lines',
            name=f"{obj.id}_path"
        ))

    return fig
