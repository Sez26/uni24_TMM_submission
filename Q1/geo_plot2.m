%% function to plot the lines between MSOA centroids and journey origin and desination data

function geo_plot2(data_MSOA,OD_mat)
    % converting nothing and easting coordinates into lat and long for
    % geoscatter plotting (using borrowed function)
    num_MSOA = length(data_MSOA.e);
    [MSOA_lat, MSOA_lon] = OSGB_to_LatLon(data_MSOA.e, data_MSOA.n);

    geoscatter(MSOA_lat, MSOA_lon, 5) % plotting centroids
    

    % creating lines between centroids
    OD_matrix = full(OD_mat);
    % OD_lines = emptylike(OD_matrix);
    for i = 1:num_MSOA
        for j = 1:num_MSOA
            geoplot(MSOA_lat([OD_matrix(i) OD_matrix(j)]),MSOA_lon([OD_matrix(i) OD_matrix(j)]), LineWidth=OD_matrix(i,j))
        end
    end

    % initialising storage array for lines
    % OD_lines = empty(numel((nonzeros(OD_mat)),1));
    % for i = 1:numel(nonzeros(OD_mat))
    %     OD_lines(i) = line(OD_mat)
    % end