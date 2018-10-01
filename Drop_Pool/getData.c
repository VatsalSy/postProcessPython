/* Title: Janus Drops
# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
*/

// Description
/* This is a post-processing code for Basilisk C generated data files
   It uses data files in the Basilisk C native binary file format (produced using)
   the "dump" command. The idea is to restore the simulation data and then interpolate the
   variables of interest on a uniform cartesian grid. and throws the output on stderr
   A python script (see DropPool.py for example) would catch the output and use
   it for post-processing
*/

#include "navier-stokes/centered.h"

scalar f1[], f2[];
char filename[80], fieldStr[80];
int nx,ny;
double xmin, ymin, xmax, ymax;
scalar * list = NULL;

event init(t = 0)
{
  restore (file = filename);
  FILE * fp = ferr;
  nx++;
  ny++;
  double Deltax = 0.999999*(xmax-xmin)/(nx - 1);
  double Deltay = 0.999999*(ymax-ymin)/(ny - 1);
  int len = list_len(list);
  double ** field = (double **) matrix_new (nx, ny, len*sizeof(double));

  for (int i = 0; i < nx; i++) {
    double x = Deltax*i + xmin;
    for (int j = 0; j < ny; j++) {
      double y = Deltay*j + ymin;
      int k = 0;
      for (scalar s in list){
        field[i][len*j + k++] = interpolate (s, x, y);
      }
    }
  }

  fprintf (fp, "# 1:x 2:y");
  int i = 3;
  for (scalar s in list){
    fprintf (fp, " %d:%s", i++, s.name);
  }
  fputc ('\n', fp);
  for (int i = 0; i < nx; i++) {
    double x = Deltax*i + xmin;
    for (int j = 0; j < ny; j++) {
      double y = Deltay*j + ymin;
      fprintf (fp, "%g %g", x, y);
      int k = 0;
      for (scalar s in list){
        fprintf (fp, " %g", field[i][len*j + k++]);
      }
      fputc ('\n', fp);
    }
  }
  fflush (fp);
  // fclose (fp);
  matrix_free (field);
}

int main(int a, char const *arguments[])
{
  sprintf (filename, "%s", arguments[1]);
  xmin = atof(arguments[2]);
  xmax = atof(arguments[3]);
  ymin = atof(arguments[4]);
  ymax = atof(arguments[5]);
  nx = atoi(arguments[6]);
  ny = atoi(arguments[7]);
  list = list_add (list, f1);
  list = list_add (list, f2);
  run();
}
