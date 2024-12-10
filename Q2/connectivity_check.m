function connectivity_check(G, s, t)
    % G: MATLAB graph object
    % vec1: Vector of starting nodes
    % vec2: Vector of target nodes

    % Compute the distance matrix
    D = distances(G);

    % Check if every node in vec1 can reach any node in vec2
    forward = all(all(D(s, t) < Inf, 2));

    % Check if every node in vec2 can reach any node in vec1
    backward = all(all(D(t, s) < Inf, 2));

    disp(['Can travel from all street nodes to all corner nodes: ', mat2str(forward)]);
    disp(['Can travel from all corner nodes to all street nodes: ', mat2str(backward)]);
end