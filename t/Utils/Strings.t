#!/usr/bin/perl

use strict;
use warnings;

use Test::More;
use FindBin qw($Bin);
use lib "$Bin/..";
use test_helper;

use Slim::Utils::Strings qw(string);

subtest 'getString' => sub {
    is(Slim::Utils::Strings::getString('NON_EXISTENT_TOKEN'), 'NON_EXISTENT_TOKEN', 'getString returns token for unknown tokens');
};

subtest 'string' => sub {
    {
        no strict 'refs';
        ${'Slim::Utils::Strings::defaultStrings'} = { 'TEST_TOKEN' => 'Hello %s' };
    }
    
    is(string('TEST_TOKEN', 'World'), 'Hello World', 'string with sprintf formatting works');
};

done_testing();
