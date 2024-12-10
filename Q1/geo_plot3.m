%%% this is the plotting function for the MSOA data plotted onto a map of
%%% the UK

function geo_plot3(data_MSOA,data_UTLA)
    % converting nothing and easting coordinates into lat and long for
    % geoscatter plotting (using borrowed function)
    num_UTLA = length(data_UTLA.e);
    % OSGB_to_LatLon function is borrowed :)
    [UTLA_lat, UTLA_lon] = OSGB_to_LatLon(data_UTLA.e, data_UTLA.n);
    [MSOA_lat, MSOA_lon] = OSGB_to_LatLon(data_MSOA.e, data_MSOA.n);
    OD_ratio = data_UTLA.D_tot./data_UTLA.O_tot; % higher ratio the more attractive a location is (more incoming than outgoing)
    [OD_ratio_s, s_idx] = sort(OD_ratio,1, "ascend");
    % Adjusting for plotting clarity
    % make attraction zones bigger markersize
    marker_size = 10.*ones(num_UTLA,1);
    % top 10% bigger
    marker_size(end-0.1*num_UTLA:end) = 30;
    
    figure;
    geoscatter(MSOA_lat, MSOA_lon, 1, "black")
    hold on
    geoscatter(UTLA_lat(s_idx), UTLA_lon(s_idx), marker_size, OD_ratio_s, 'filled') % colour depending on O/D ratio


    cb = colorbar(); 
    ylabel(cb,'Total Journey Destinations/Total Journey Origins','Rotation',270)
    colormap(jet); % Choose a colormap (e.g., 'jet', 'parula', etc.)
    clim([min(OD_ratio), max(OD_ratio)]); % Optional: Set the color axis limits
    


