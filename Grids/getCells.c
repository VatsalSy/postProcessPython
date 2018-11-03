/* Title: Getting Grid Cells 
# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
*/
#include "fractions.h"
#include "navier-stokes/centered.h"


scalar f[];
face vector sf[];
char filename[80];
int main(int a, char const *arguments[])
{
  sprintf (filename, "%s", arguments[1]);
  restore (file = filename);
  #if TREE
    f.prolongation = fraction_refine;
  #endif
  boundary(all);
  // face_fraction(f,sf);
  FILE * fp = ferr;
  output_cells (fp);
  fflush (fp);
  fclose (fp);
}
