function [] = gen3D()
    %gets the range of files to be opened
    disp('Select one of the following:');
    disp('1. Plotting one 3D terrain map');
    disp('2. Plot the difference between to terrain maps');
    disp('3. Plotting a 2D terrain map');
    plotType = input('');
    
    if plotType == 1 || plotType == 4
        lowerBound = input('Enter first iteration to be read in: ');
        
        [x,y,z] = readIn(num2str(lowerBound),0);                        %reads in the latitudes, longitudes, and altitudes
        meshable(x,y,z,'Virginia Barrier Islands Data',1,1,plotType);   %creates the 3D terrain model or a 2D terrain map
    else
        lowerBound = input('Enter first iteration to be read in: ');
        upperBound = input('Enter last iteration to be read in: ');
        
        
        [x0,y0,z0] = readIn(num2str(lowerBound),0);                          %reads in the latitudes, longitudes, and altitudes
        [x01,y01,z01] = readIn(num2str(lowerBound),1);                     %reads in the latitudes, longitudes, and altitudes of the empty resized matrix

        [x1,y1,z1] = readIn(num2str(upperBound),0);                          %reads in the latitudes, longitudes, and altitudes
        [x11,y11,z11] = readIn(num2str(lowerBound),1);                     %reads in the latitudes, longitudes, and altitudes of the empty resized matrix

        [matrix1,matrix2] = resize(z0,z01,z1,z11);
        disp('Matrices new dimensions:')
        disp(size(matrix1))
        disp(size(matrix2))
        i = matrix1 - matrix2;       %gets the difference between the first and last matrix read in (given they have the same dimensions)
        meshable(x01,y01,i,'Change of the Island',1,1,plotType)
    end

    
    %reads in all the text files specified and creates the 3D terrain
    %models
%     i = lowerBound;
%     
%     %sets the number of plots to be created
%     if lowerBound == upperBound
%         tot = 1;
%     else
%         tot = 2;
%     end
    
    
    
%     while i <= upperBound
%         %x = latitudes
%         %y = longitudes
%         %z = matrix of altitudes
%         [x,y,z] = readIn(num2str(i));     %reads in the latitudes, longitudes, and altitudes
%         
%         %creates the 3D terrain model
%         if i == lowerBound
%         meshable(x,y,z,'Virginia Barrier Islands Data',1,tot,plotType);
%         end
%         hold on
%         i = i + 1;
%     end
%    hold off  %displays all data on the same chart 
%     
%     if tot == 2
%        [x,y,a] = readIn(num2str(lowerBound));
%        [x,y,b] = readIn(num2str(upperBound));
%        z = a - b;       %gets the difference between the first and last matrix read in (given they have the same dimensions)
%        meshable(x,y,z,'Change of the Island',2,tot,plotType)
%     end
    
    
end

%reads in the the latitudes, longitudes, and the matrix containing the
%altitudes
function [lats,longs,matrix] = readIn(iteration,isSized)
    if isSized == 0
        %reads lats and longs in vectors
        lats  = csvread(strcat('3D Latitudes(',iteration,').txt'));
        longs   = csvread(strcat('3D Longitudes(',iteration,').txt'));
        
        %reads matrix from text file into a matrix
        matrix = csvread(strcat('3D Matrix(',iteration,').txt'));
    else
        %reads lats and longs in vectors
        lats  = csvread(strcat('3D Latitudes(resized)(',iteration,').txt'));
        longs   = csvread(strcat('3D Longitudes(resized)(',iteration,').txt'));
        
        %reads matrix from text file into a matrix
        matrix = csvread(strcat('3D Matrix(resized)(',iteration,').txt'));
    end
    
    %displays the amount of data read in
    disp(size(matrix));
    disp(size(longs));
    disp(size(lats));
end

%creates a 3D terrain model using the two vectors and a matrix
function [] = meshable(x,y,z,t,subPlot,tot,plotType)
    if plotType == 1 || plotType == 2
        [X,Y] = meshgrid(y,x);                %converts x,y vectors to
                                               %matrices
        set(gcf, 'renderer' , 'zbuffer');
        subplot(1,tot,subPlot)                %creates a subplot if necessary
        disp(size(X))
        disp(size(Y))
        disp(size(z))
        h = surf(X,Y,z);                      %creates 3D model
        set(h,'LineStyle','none');            %gets rid of excess lines
        is3D = true;                          %TRUE = 3D model     FALSE = 2D image

    else
        imagesc(z)                            %creates a top down 2D image
    end
    colorbar;                             %creates a scale on the right
    colormap(parula(5));                  %adds the color map to the image/model
    
    %labels
    title(t);
    xlabel('Longitudes')
    ylabel('Latitudes')
    zlabel('Altitudes')
    
    %saves the figure
%     if is3D == true
%         savefig(strcat('./figures/3D Model(',iteration,').fig'))
%     else
%         savefig(strcat('./figures/2D Model(',iteration,').fig'))
% 
%     end
end

%resizes the matrix and scales the elements apropriately
function [m11,m22] = resize(m1,m11,m2,m22)
xInc = max(length(m1(1)),length(m2(1)));    %gets the largest width
yInc = max(length(m1),length(m2));          %gets the largest height

%how much larger each of the matrices dimensions need to be
x1 = xInc/length(m1(1));
x2 = xInc/length(m2(1));
y1 = yInc/length(m1);
y2 = yInc/length(m2);

i = 1;
while i < length(m1(1))        %resizes the m1 matrix to fit the new dimension horizontally
   row = m1(i,:); %gets the row
   x = repelem(row,uint8(x1));
   if length(x) == length(m11)
        m11 = x;
   else
       j = abs(length(m11) - length(x));       
       temp = uint8(j/2);
       m11.arraypad(temp,0,0,'post');
       m11.arraypad(temp-j,0,0,'pre');           
   end
   i = i + 1;
end

i = 1;
while i < length(m1(1))     %resizes the m1 matrix to fit the new dimension vertically
   col = m11(:,i);   %gets the column
   x(:,i) = repelem(col,uint8(y1));
   if length(x) == length(m11)
       m11(i) = x;
   else
       j = abs(length(m22) - length(x));       
       temp = uint8(j/2);
       m11.arraypad(0,temp,0,'post');
       m11.arraypad(0,temp-j,0,'pre');           
   end
   i = i + 1;
end

i = 1;
while i < length(m2(1))        %resizes the m2 matrix to fit the new dimension horizontally
   row = m2(i,:); %gets the row
   x(i) = repelem(row,uint8(x2));
   if length(x) == length(m11)
        m22 = x;
   else
       j = abs(length(m22) - length(x));       
       temp = uint8(j/2);
       m22.arraypad(temp,0,0,'post');
       m22.arraypad(temp-j,0,0,'pre');           
   end
   i = i + 1;
end

i = 1;
while i < length(m2(1))     %resizes the m2 matrix to fit the new dimension vertically
   col = m2(:,i);   %gets the column
   x(:,i) = repelem(col,uint8(y2));
   if length(x) == length(m22)
        m22(i) = x;
   else
       j = abs(length(m22) - length(x));       
       temp = uint8(j/2);
       m22.arraypad(0,temp,0,'post');
       m22.arraypad(0,temp-j,0,'pre');           
   end
   i = i + 1;
end
end









