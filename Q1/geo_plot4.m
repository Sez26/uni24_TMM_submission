% I want this to visualise the bloat of markers for the people who don't
% leave the city, and the top 5 lines between each MSOA with line thickness
% and colour
function geo_plot4(data_MSOA)
    num_MSOA = length(data_MSOA.e);
    [bris_idx,bris_names] = get_bris_MSOA(data_MSOA);
    bris_OD = data_MSOA.OD_mat(bris_idx,bris_idx);
    [MSOA_lat, MSOA_lon] = OSGB_to_LatLon(data_MSOA.e(bris_idx), data_MSOA.n(bris_idx));
    
    % find people who stay home, ie diagonal count
    rest_O = diag(bris_OD);
    % normalise and make markersize 
    max_marker = 150;
    min_marker = 10;
    marker_size = floor(rest_O.*((max_marker-min_marker)/(max(rest_O,[],"all")-min(rest_O,[],"all")))+min_marker);
    % Plot all lines
    figure;
    % Loop through each pair of origin and destination
    cmap = jet;
    colorLimits = [min(bris_OD,[],"All"), max(bris_OD,[],"All")]; % Color limits based on demand range

    [numOrigins, numDestinations] = size(bris_OD);

    % sort to get top counts
    [top_D, s_idx] = sort(bris_OD,1, "descend");

    % maybe only plot the top 3 lines
    for i = 1:numOrigins
        for j = 2:4 % excluding self jouney
            % Get the journey count
            journeyCount = bris_OD(i, s_idx(j));
            colorIdx = (journeyCount - colorLimits(1)) / (colorLimits(2) - colorLimits(1)); % Normalize demand
            if journeyCount > 0
               % Plot a line with thickness proportional to journey count
                geoplot([MSOA_lat(i), MSOA_lat(s_idx(j))], [MSOA_lon(i), MSOA_lon(s_idx(j))], ...
                'LineWidth', 1.5, 'Color', cmap(round(colorIdx * (size(cmap, 1) - 1)) + 1, :)); % Line color
            end
            hold on
        end
    end
    geoscatter(MSOA_lat, MSOA_lon, marker_size, 'filled', 'Color', 'k')
    colorbar;