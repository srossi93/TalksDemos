$clean_ext .= ' %R.figlist %R-figure* %R.makefile fls.tmp';
$latex    = 'internal tikzlatex latex    %B %O %S';
$pdflatex = 'internal tikzlatex pdflatex %B %O %S';
$lualatex = 'internal tikzlatex lualatex %B %O %S';
$xelatex  = 'internal tikzlatex xelatex  %B %O %S';
$hash_calc_ignore_pattern{'pdf'} = '^(/CreationDate|/ModDate|/ID)';
$hash_calc_ignore_pattern{'ps'} = '^%%CreationDate';

sub tikzlatex {
  my ($engine, $base, @args) = @_;
  my $ret = 0;
  print "\nTikzlatex: ===Running '$engine @args'...\n";
  $ret = system( $engine, @args );
  print "\nTikzlatex: Fixing .fls file ...\n";
  system "echo INPUT \"$aux_dir1$base.figlist\"  >  \"$aux_dir1$base.fls.tmp\"";
  system "echo INPUT \"$aux_dir1$base.makefile\" >> \"$aux_dir1$base.fls.tmp\"";
  system "cat \"$aux_dir1$base.fls\"    >> \"$aux_dir1$base.fls.tmp\"";
  rename "$aux_dir1$base.fls.tmp", "$aux_dir1$base.fls";
  if ($ret) { return $ret; }
  if ( -e "$aux_dir1$base.makefile" ) {
    if ($engine eq 'xelatex') {
      print "\nTikzlatex: ---Correcting '$aux_dir1$base.makefile' made under xelatex\n";
      system( 'perl', '-i', '-p', '-e', 's/^\^\^I/\t/', "$aux_dir1$base.makefile" );
    }
    elsif ($engine eq 'latex') {
      print "\nTikzlatex: ---Correcting '$aux_dir1$base.makefile' made under latex\n";
      system( 'perl', '-i', '-p', '-e', 's/\.epsi/\.ps/', "$aux_dir1$base.makefile" );
    }
    print "\nTikzlatex: ---Running 'make -f $aux_dir1$base.makefile' ...\n";
    if ($aux_dir) {
      # latexmk has set $ENV{TEXINPUTS} in this case.
      my $SAVETEXINPUTS = $ENV{TEXINPUTS};
      $ENV{TEXINPUTS} = good_cwd().$search_path_separator.$ENV{TEXINPUTS};
      pushd( $aux_dir );
      $ret = system "make",  "-j8",  "-f", "$base.makefile";
      &popd;
      $ENV{TEXINPUTS} = $SAVETEXINPUTS;
    }
    else {
      $ret = system "make",  "-j8",  "-f", "$base.makefile";
    }
    if ($ret) {
      print "\nTikzlatex: !!!!!!!!!!!!!! Error from make !!!!!!!!! \n",
            "  The log files for making the figures '$aux_dir1$base-figure*.log'\n",
            "  may have information\n";
    }
  }
  else {
    print "\nTikzlatex: No '$aux_dir1$base.makefile', so I won't run make.\n";
  }
  return $ret;
}
