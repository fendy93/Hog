test = {
  'names': [
    'q00',
    '0',
    'q0'
  ],
  'points': 0,
  'suites': [
    [
      {
        'locked': True,
        'test': """
        >>> test_dice = make_test_dice(4, 1, 2)
        >>> test_dice()
        8d709cc2e9b8b2de8355f2111daac7e0
        # locked
        >>> test_dice() # Second call
        e68cec39a1f8cdadbbcff3001223250a
        # locked
        >>> test_dice() # Third call
        01c33be5741340470bed9013039733b5
        # locked
        >>> test_dice() # Fourth call
        8d709cc2e9b8b2de8355f2111daac7e0
        # locked
        """,
        'type': 'doctest'
      }
    ]
  ]
}