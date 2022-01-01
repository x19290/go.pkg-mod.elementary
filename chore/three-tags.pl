#!/usr/bin/env perl

# 1.
#    edit tags in README.md
#    git rm -rf 1 2
#    git commit -a -m "chore: ..."
#
# 2. (python3 moddemo.py)
#    make changes
#    git commit -a -m "chore: ..."
#    make more changes
#
# 3.
#    git commit -a -m "chore: ..."
#    git tag ~.seed HEAD^^
#    git tag ~.go-mod/edit HEAD^
#    git tag ~.go-mod/tidy HEAD

use Cwd 'abs_path';
use File::Basename 'dirname';
use File::Slurp 'write_file';
use strict;
use warnings;

chdir(dirname dirname abs_path(__FILE__));

open my $tags, 'git tag |';

my $c = $b = $a = '-';
while (my $new = <$tags>) {
	chomp $new;
	$a = $b;
	$b = $c;
	$c = $new;
}
my $tag_prefix = $a;
$tag_prefix =~ s/.\..*$//;
my $new_prefix = $tag_prefix;
$new_prefix++;  # i chosed perl only for this operation

$a = substr $a, 1;
$b = substr $b, 1;
$c = substr $c, 1;

my $qa = qr/\b\Q$tag_prefix$a\E\b/;
my $qb = qr/\b\Q$tag_prefix$b\E\b/;
my $qc = qr/\b\Q$tag_prefix$c\E\b/;
my $na = "$new_prefix$a";
my $nb = "$new_prefix$b";
my $nc = "$new_prefix$c";

open my $err, '>&', *STDERR;
{
	close *STDERR;
	system "git tag -d $na";
	system "git tag -d $nb";
	system "git tag -d $nc";
}
open *STDERR, '>&', $err;
close $err;

my @readme;
open my $readme, 'README.md';
while (my $line = <$readme>) {
	$line =~ s/$qa/$na/;
	$line =~ s/$qb/$nb/;
	$line =~ s/$qc/$nc/;
	push @readme, $line;
}

# 1.
write_file 'README.md', @readme;
system 'git rm -rf 1 2';
system qw(git commit -a -m), "chore: make `$na`";
# 2.
system 'python3 moddemo.py';
# 3.
system qw(git commit -a -m), "chore: go mod tidy";
system "git tag $na HEAD^^";
system "git tag $nb HEAD^";
system "git tag $nc HEAD";
