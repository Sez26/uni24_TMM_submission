function plotNetwork(G, x, nodeCoordinates, ax)
    % G is the graph object
    % x is the vector of link flows
    % nodeCoordinates is a 1000x2 matrix with the (x, y) positions of the nodes

    % Constant line width for all edges
    constantLineWidth = 1;  % You can adjust this value as desired

    % Create the plot object with constant line width
    p = plot(ax, G, 'LineWidth', constantLineWidth);

    % Set custom node positions using nodeCoordinates
    p.XData = nodeCoordinates(:, 1);  % X-coordinates of nodes
    p.YData = nodeCoordinates(:, 2);  % Y-coordinates of nodes
    
    % Set node color and marker size
    p.NodeColor = [0, 0, 0];   % Black color for nodes
    p.MarkerSize = 1;

    % Create the color mapping based on link flows (from white for 0 to red for max flow)
    maxFlow = max(x);
    flowNormalized = x / maxFlow;  % Normalize flow values between 0 and 1

    % % Normalize flow values using a logarithmic scale
    % flowNormalized = log10(x + 1);  % +1 to avoid log(0) if there are zero flows
    % flowNormalized = flowNormalized / max(flowNormalized);  % Normalize to [0, 1]

    % Set up the color data for edges
    % Create an array of color values, with 0 flow being white, and non-zero flows mapped to the colormap
    EdgeColors = ones(numel(x), 3);  % Default to white
    nonZeroFlows = flowNormalized > 0;  % Find the non-zero flows
    
    % Apply the colormap to non-zero flows
    EdgeColors(nonZeroFlows, :) = repmat(flowNormalized(nonZeroFlows), 1, 3);  % Use the normalized flow to assign color
    
    % Apply the colormap ranging from white (for 0 flow) to red (for max flow)
    % colormap('hot'); 
    colormap(flipud('hot'))

    % Set edge color based on the flow values
    % p.EdgeColor = 'flat';  % Allow using flat color data
    p.EdgeCData = flowNormalized;  % Assign the edge color data

    % Display the colorbar to show the flow-color mapping
    colorbar;  % Show the colorbar
    clim([0 1]);  % Set the color scale to match normalized flow values (0 to 1)

    % Set the axis limits to ensure everything fits
    axis tight;
    % title('Network with Node Coordinates and Flow-based Edge Color');
end
