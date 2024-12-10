%%% this is the plotting function for the MSOA data plotted onto a map of
%%% the UK

function geo_plot1(data_MSOA)
    % converting nothing and easting coordinates into lat and long for
    % geoscatter plotting (using borrowed function)
    num_MSOA = length(data_MSOA.e);
    [MSOA_lat, MSOA_lon] = OSGB_to_LatLon(data_MSOA.e, data_MSOA.n);
    OD_ratio = data_MSOA.D_tot./data_MSOA.O_tot; % higher ratio the more attractive a location is (more incoming than outgoing)
    [OD_ratio_s, s_idx] = sort(OD_ratio,1, "ascend");
    % Adjusting for plotting clarity
    % cut off all below 1 to be lower limit
    % low_ODratio = find(OD_ratio<1);
    % OD_ratio(low_ODratio) = 0.5;
    % make attraction zones bigger markersize
    marker_size = 5.*ones(num_MSOA,1);
    % top 10% bigger
    marker_size(end-0.1*num_MSOA:end) = 20;

    geoscatter(MSOA_lat(s_idx), MSOA_lon(s_idx), marker_size, OD_ratio_s, 'filled') % colour depending on O/D ratio

    cb = colorbar(); 
    ylabel(cb,'Total Journey Destinations/Total Journey Origins','Rotation',270)
    colormap(jet); % Choose a colormap (e.g., 'jet', 'parula', etc.)
    clim([min(OD_ratio), max(OD_ratio)]); % Optional: Set the color axis limits
    


