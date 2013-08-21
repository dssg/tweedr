import logging
logger = logging.getLogger(__name__)


class Pipeline(object):
    def __init__(self, *mappers):
        logger.info('%s -> [pipeline] -> %s', mappers[0].INPUT, mappers[-1].OUTPUT)
        # type-check the connections between the provided mappers
        total_errors = 0
        for from_pipe, to_pipe in zip(mappers, mappers[1:]):
            # Python lets you use `a <= b` to say `a is a subclass of b`
            # SuperClass >= Class is true
            # Class >= Class is true
            # Class >= SuperClass is false
            if from_pipe.OUTPUT < to_pipe.INPUT:
                logger.error('Pipeline cannot connect mappers: %s[%s] -> %s[%s]',
                    from_pipe.__class__.__name__, from_pipe.OUTPUT.__name__,
                    to_pipe.__class__.__name__, to_pipe.INPUT.__name__)
                total_errors += 1
        if total_errors > 0:
            raise TypeError('Pipeline types do not match.')
        self.mappers = mappers

    def __call__(self, payload):
        logger.notset('Pipeline processing payload: %s', payload)
        # TODO: maybe wrap with a try-except here?
        for mapper in self.mappers:
            payload = mapper(payload)
            if payload is None:
                break
        return payload
