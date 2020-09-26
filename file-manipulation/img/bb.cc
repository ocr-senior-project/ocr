// Compute horizontal projections
   Mat1f horProj;
   reduce(rotated, horProj, 1, CV_REDUCE_AVG);

   // Remove noise in histogram. White bins identify space lines, black bins identify text lines
   float th = 0;
   Mat1b hist = horProj <= th;

   // Get mean coordinate of white white pixels groups
   vector<int> ycoords;
   int y = 0;
   int count = 0;
   bool isSpace = false;
   for (int i = 0; i < rotated.rows; ++i)
   {
       if (!isSpace)
       {
           if (hist(i))
           {
               isSpace = true;
               count = 1;
               y = i;
           }
       }
       else
       {
           if (!hist(i))
           {
               isSpace = false;
               ycoords.push_back(y / count);
           }
           else
           {
               y += i;
               count++;
           }
       }
   }

   // Draw line as final result
   Mat3b result;
   cvtColor(rotated, result, COLOR_GRAY2BGR);
   for (int i = 0; i < ycoords.size(); ++i)
   {
       line(result, Point(0, ycoords[i]), Point(result.cols, ycoords[i]), Scalar(0, 255, 0));
   }

   return 0;
}
